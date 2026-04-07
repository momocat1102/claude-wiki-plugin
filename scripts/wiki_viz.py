#!/usr/bin/env python3
"""
LLM Wiki Visualization Generator

Generates knowledge graphs, stats charts, timelines, and coverage maps
from a wiki directory structure.

Usage:
    python wiki_viz.py --wiki-dir <path> --type <graph|stats|timeline|coverage> [--output <path>]

Dependencies (auto-installed if missing):
    pip install matplotlib networkx pyyaml
"""

import argparse
import re
import sys
import subprocess
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

# Auto-install dependencies
def ensure_deps():
    for pkg, import_name in [("matplotlib", "matplotlib"), ("networkx", "networkx"), ("pyyaml", "yaml")]:
        try:
            __import__(import_name)
        except ImportError:
            print(f"Installing {pkg}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

ensure_deps()

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import yaml


def parse_frontmatter(filepath: Path) -> dict:
    """Extract YAML frontmatter from a markdown file."""
    text = filepath.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def extract_links(filepath: Path, wiki_dir: Path) -> list[str]:
    """Extract wikilinks ([[page-name]]) and standard markdown links."""
    text = filepath.read_text(encoding="utf-8")
    links = []

    # Obsidian wikilinks: [[page-name]] or [[page-name|Display Text]]
    for match in re.finditer(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", text):
        target = match.group(1).strip()
        # Skip image embeds
        if target.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")):
            continue
        links.append(target)

    # Standard markdown links: [text](path.md) (fallback)
    for match in re.finditer(r"\[([^\]]+)\]\(([^)]+\.md)\)", text):
        target = match.group(2)
        resolved = (filepath.parent / target).resolve()
        try:
            rel = resolved.relative_to(wiki_dir.resolve())
            links.append(str(rel))
        except ValueError:
            pass

    return links


def scan_wiki(wiki_dir: Path) -> list[dict]:
    """Scan all markdown files in the wiki directory."""
    pages = []
    for md_file in sorted(wiki_dir.rglob("*.md")):
        rel_path = md_file.relative_to(wiki_dir)
        fm = parse_frontmatter(md_file)
        links = extract_links(md_file, wiki_dir)
        category = rel_path.parts[0] if len(rel_path.parts) > 1 else "root"
        pages.append({
            "path": str(rel_path),
            "name": fm.get("title", md_file.stem),
            "type": fm.get("type", "unknown"),
            "tags": fm.get("tags", []) or [],
            "status": fm.get("status", "unknown"),
            "created": fm.get("created", ""),
            "updated": fm.get("updated", ""),
            "sources": fm.get("sources", []) or [],
            "category": category,
            "links": links,
        })
    return pages


def generate_graph(pages: list[dict], output: Path):
    """Generate a knowledge graph visualization."""
    G = nx.DiGraph()

    category_colors = {
        "entities": "#4ECDC4",
        "concepts": "#FF6B6B",
        "sources": "#95E1D3",
        "analyses": "#F38181",
        "root": "#FCE38A",
    }

    for page in pages:
        if page["path"] in ("index.md", "log.md"):
            continue
        color = category_colors.get(page["category"], "#AAAAAA")
        G.add_node(page["path"], label=page["name"], color=color, category=page["category"])

    for page in pages:
        for link in page["links"]:
            if link in G.nodes and page["path"] in G.nodes:
                G.add_edge(page["path"], link)

    if len(G.nodes) == 0:
        print("No pages to graph.")
        return

    fig, ax = plt.subplots(1, 1, figsize=(16, 12), facecolor="#1a1a2e")
    ax.set_facecolor("#1a1a2e")

    pos = nx.spring_layout(G, k=2.5, iterations=50, seed=42)
    colors = [G.nodes[n].get("color", "#AAAAAA") for n in G.nodes]
    labels = {n: G.nodes[n].get("label", n)[:20] for n in G.nodes}

    # Draw edges
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#ffffff30", arrows=True,
                           arrowsize=10, width=0.8, connectionstyle="arc3,rad=0.1")
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=colors, node_size=800,
                           alpha=0.9, edgecolors="#ffffff50", linewidths=1.5)
    # Draw labels
    nx.draw_networkx_labels(G, pos, labels=labels, ax=ax, font_size=7,
                            font_color="white", font_weight="bold")

    # Legend
    legend_handles = [mpatches.Patch(color=c, label=cat.title())
                      for cat, c in category_colors.items() if cat in {p["category"] for p in pages}]
    ax.legend(handles=legend_handles, loc="upper left", fontsize=10,
              facecolor="#16213e", edgecolor="#ffffff30", labelcolor="white")

    ax.set_title("Wiki Knowledge Graph", fontsize=18, color="white", pad=20)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches="tight", facecolor="#1a1a2e")
    plt.close()
    print(f"Graph saved to {output}")


def generate_stats(pages: list[dict], output: Path):
    """Generate statistics charts."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), facecolor="#1a1a2e")
    for ax in axes.flat:
        ax.set_facecolor("#16213e")

    colors = ["#4ECDC4", "#FF6B6B", "#95E1D3", "#F38181", "#FCE38A", "#AA96DA"]

    # 1. Pages by category
    cat_counts = Counter(p["category"] for p in pages if p["path"] not in ("index.md", "log.md"))
    if cat_counts:
        cats, counts = zip(*sorted(cat_counts.items(), key=lambda x: -x[1]))
        bars = axes[0, 0].barh(cats, counts, color=colors[:len(cats)])
        axes[0, 0].set_title("Pages by Category", color="white", fontsize=12)
        axes[0, 0].tick_params(colors="white")
        for bar, count in zip(bars, counts):
            axes[0, 0].text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
                            str(count), va="center", color="white", fontsize=10)

    # 2. Status distribution
    status_counts = Counter(p["status"] for p in pages if p["status"] != "unknown")
    if status_counts:
        labels, sizes = zip(*status_counts.items())
        axes[0, 1].pie(sizes, labels=labels, colors=colors[:len(labels)],
                       autopct="%1.0f%%", textprops={"color": "white"})
        axes[0, 1].set_title("Page Status Distribution", color="white", fontsize=12)

    # 3. Top tags
    all_tags = [tag for p in pages for tag in p["tags"]]
    tag_counts = Counter(all_tags).most_common(10)
    if tag_counts:
        tags, counts = zip(*tag_counts)
        axes[1, 0].barh(tags, counts, color="#4ECDC4")
        axes[1, 0].set_title("Top 10 Tags", color="white", fontsize=12)
        axes[1, 0].tick_params(colors="white")

    # 4. Link density
    link_counts = [(p["name"][:15], len(p["links"])) for p in pages
                   if p["path"] not in ("index.md", "log.md") and len(p["links"]) > 0]
    link_counts.sort(key=lambda x: -x[1])
    link_counts = link_counts[:10]
    if link_counts:
        names, counts = zip(*link_counts)
        axes[1, 1].barh(names, counts, color="#FF6B6B")
        axes[1, 1].set_title("Most Connected Pages", color="white", fontsize=12)
        axes[1, 1].tick_params(colors="white")

    for ax in axes.flat:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_color("#ffffff30")
        ax.spines["left"].set_color("#ffffff30")

    plt.suptitle("Wiki Statistics", fontsize=16, color="white", y=1.02)
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches="tight", facecolor="#1a1a2e")
    plt.close()
    print(f"Stats saved to {output}")


def generate_timeline(pages: list[dict], output: Path):
    """Generate a timeline of source ingestion."""
    sources = [p for p in pages if p["category"] == "sources" and p["created"]]

    if not sources:
        print("No dated sources found for timeline.")
        return

    # Parse dates
    dated = []
    for s in sources:
        try:
            d = datetime.strptime(str(s["created"]), "%Y-%m-%d")
            dated.append((d, s["name"]))
        except (ValueError, TypeError):
            pass

    if not dated:
        print("No valid dates found.")
        return

    dated.sort()

    fig, ax = plt.subplots(figsize=(16, max(4, len(dated) * 0.4)), facecolor="#1a1a2e")
    ax.set_facecolor("#16213e")

    dates = [d[0] for d in dated]
    names = [d[1][:40] for d in dated]
    y_positions = range(len(dated))

    ax.scatter(dates, y_positions, color="#4ECDC4", s=80, zorder=3)
    ax.hlines(y_positions, min(dates), dates, color="#4ECDC430", linewidth=1)

    ax.set_yticks(list(y_positions))
    ax.set_yticklabels(names, fontsize=9, color="white")
    ax.tick_params(axis="x", colors="white")

    ax.set_title("Source Ingestion Timeline", fontsize=16, color="white", pad=15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_color("#ffffff30")
    ax.spines["left"].set_color("#ffffff30")

    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches="tight", facecolor="#1a1a2e")
    plt.close()
    print(f"Timeline saved to {output}")


def generate_coverage(pages: list[dict], output: Path):
    """Generate a topic coverage heatmap based on tags."""
    tag_status = defaultdict(lambda: {"stub": 0, "draft": 0, "solid": 0, "comprehensive": 0})

    for p in pages:
        status = p["status"] if p["status"] in ("stub", "draft", "solid", "comprehensive") else "stub"
        for tag in p["tags"]:
            tag_status[tag][status] += 1

    if not tag_status:
        print("No tagged pages found for coverage map.")
        return

    # Sort by total pages
    sorted_tags = sorted(tag_status.items(), key=lambda x: -sum(x[1].values()))[:15]

    fig, ax = plt.subplots(figsize=(12, max(4, len(sorted_tags) * 0.5)), facecolor="#1a1a2e")
    ax.set_facecolor("#16213e")

    statuses = ["stub", "draft", "solid", "comprehensive"]
    status_colors = {"stub": "#FF6B6B", "draft": "#FCE38A", "solid": "#95E1D3", "comprehensive": "#4ECDC4"}

    tags = [t[0] for t in sorted_tags]
    y_pos = range(len(tags))
    left = [0] * len(tags)

    for status in statuses:
        widths = [sorted_tags[i][1][status] for i in range(len(tags))]
        ax.barh(y_pos, widths, left=left, color=status_colors[status], label=status, height=0.6)
        left = [left[i] + widths[i] for i in range(len(tags))]

    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(tags, fontsize=10, color="white")
    ax.tick_params(axis="x", colors="white")
    ax.set_title("Topic Coverage Map", fontsize=16, color="white", pad=15)
    ax.legend(fontsize=9, facecolor="#16213e", edgecolor="#ffffff30", labelcolor="white")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_color("#ffffff30")
    ax.spines["left"].set_color("#ffffff30")

    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches="tight", facecolor="#1a1a2e")
    plt.close()
    print(f"Coverage map saved to {output}")


def main():
    parser = argparse.ArgumentParser(description="LLM Wiki Visualization Generator")
    parser.add_argument("--wiki-dir", required=True, help="Path to the wiki/ directory")
    parser.add_argument("--type", choices=["graph", "stats", "timeline", "coverage"],
                        default="graph", help="Type of visualization")
    parser.add_argument("--output", help="Output file path (default: wiki/assets/<type>.png)")
    args = parser.parse_args()

    wiki_dir = Path(args.wiki_dir)
    if not wiki_dir.exists():
        print(f"Error: {wiki_dir} does not exist")
        sys.exit(1)

    pages = scan_wiki(wiki_dir)
    print(f"Scanned {len(pages)} pages")

    # Determine output path
    if args.output:
        output = Path(args.output)
    else:
        assets_dir = wiki_dir / "assets"
        assets_dir.mkdir(exist_ok=True)
        output = assets_dir / f"{args.type}.png"

    output.parent.mkdir(parents=True, exist_ok=True)

    generators = {
        "graph": generate_graph,
        "stats": generate_stats,
        "timeline": generate_timeline,
        "coverage": generate_coverage,
    }

    generators[args.type](pages, output)


if __name__ == "__main__":
    main()
