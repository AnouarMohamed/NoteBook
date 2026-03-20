from pathlib import Path

from mot_pricing import run_two_uniform_experiment, save_experiment_artifacts
from mot_pricing.gallery import GallerySpec, gallery_rows, render_gallery_markdown, save_gallery_assets


def test_save_experiment_artifacts_writes_expected_files(tmp_path: Path):
    experiment = run_two_uniform_experiment(
        x_interval=(1.0, 3.0),
        y_interval=(0.0, 4.0),
        n=10,
        payoff_name="abs_spread",
        eps_values=(0.3, 0.1),
    )

    save_experiment_artifacts(tmp_path, experiment)

    assert (tmp_path / "exact_uniform_summary.png").exists()
    assert (tmp_path / "regularization_path.png").exists()
    assert (tmp_path / "stability_diagnostics.png").exists()
    assert (tmp_path / "structural_diagnostics.png").exists()
    assert (tmp_path / "summary.json").exists()
    assert (tmp_path / "experiment_report.md").exists()


def test_save_gallery_assets_writes_gallery_summary(tmp_path: Path):
    specs = (
        GallerySpec(
            slug="small_abs",
            title="Small abs spread",
            description="Test case",
            x_interval=(1.0, 3.0),
            y_interval=(0.0, 4.0),
            n=8,
            payoff_name="abs_spread",
            eps_values=(0.3,),
        ),
        GallerySpec(
            slug="small_call",
            title="Small call spread",
            description="Test case",
            x_interval=(1.0, 3.0),
            y_interval=(0.0, 4.0),
            n=8,
            payoff_name="call_on_spread",
            strike=0.25,
            eps_values=(0.3,),
        ),
    )

    entries = save_gallery_assets(tmp_path, specs)

    assert len(entries) == 2
    assert (tmp_path / "gallery_overview.png").exists()
    assert (tmp_path / "gallery_summary.json").exists()
    assert (tmp_path / "gallery_summary.md").exists()
    assert (tmp_path / "gallery_casebook.md").exists()
    assert (tmp_path / "small_abs" / "summary.json").exists()
    assert (tmp_path / "small_call" / "summary.json").exists()
    assert (tmp_path / "small_abs" / "experiment_report.md").exists()


def test_render_gallery_markdown_contains_example_titles(tmp_path: Path):
    specs = (
        GallerySpec(
            slug="demo",
            title="Demo example",
            description="Demo",
            x_interval=(1.0, 3.0),
            y_interval=(0.0, 4.0),
            n=8,
            payoff_name="abs_spread",
            eps_values=(0.3,),
        ),
    )
    rows = gallery_rows(save_gallery_assets(tmp_path, specs))
    markdown = render_gallery_markdown(rows)

    assert "Demo example" in markdown
    assert "Smallest eps" in markdown


def test_gallery_casebook_contains_links_and_titles(tmp_path: Path):
    specs = (
        GallerySpec(
            slug="demo",
            title="Demo example",
            description="Demo",
            x_interval=(1.0, 3.0),
            y_interval=(0.0, 4.0),
            n=8,
            payoff_name="abs_spread",
            eps_values=(0.3,),
        ),
    )
    save_gallery_assets(tmp_path, specs)
    casebook = (tmp_path / "gallery_casebook.md").read_text(encoding="utf-8")

    assert "Demo example" in casebook
    assert "structural_diagnostics.png" in casebook
