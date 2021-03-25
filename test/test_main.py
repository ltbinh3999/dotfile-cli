from click.testing import CliRunner
from src.main import dfm
import pytest
import pickle


DATABASE_NAME = ".data"
# TODO: Fix all exit code assertion with specific exception


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


@pytest.fixture(scope="module")
def sample_add_data():
    return [
        ("/.config/fish.config", "fish"),
        ("/.config/.gitconfig", "git"),
        ("/.config/rofi.rasi", "rofi"),
    ]


class TestDelete:
    def test_no_name_in_database(self, runner, sample_add_data):
        with runner.isolated_filesystem():
            with open(DATABASE_NAME, "wb+") as f:
                pickle.dump(sample_add_data, f)
            result = runner.invoke(dfm, ["delete", "kitty"])
            assert 2 == result.exit_code

    def test_name_in_database(self, runner, sample_add_data):
        with runner.isolated_filesystem():
            with open(DATABASE_NAME, "wb+") as f:
                pickle.dump(sample_add_data, f)
            runner.invoke(dfm, ["delete", "git"])
            with open(DATABASE_NAME, "rb") as f:
                assert [sample_add_data[0], sample_add_data[2]] == pickle.load(f)
            runner.invoke(dfm, ["delete", "fish"])
            with open(DATABASE_NAME, "rb") as f:
                assert [sample_add_data[2]] == pickle.load(f)
            runner.invoke(dfm, ["delete", "rofi"])
            with open(DATABASE_NAME, "rb") as f:
                assert [] == pickle.load(f)


class TestAdd:
    def test_single_data(self, runner, sample_add_data):
        pass

    def test_multiple_data(self, runner, sample_add_data):
        with runner.isolated_filesystem():
            for src, name in sample_add_data:
                result = runner.invoke(
                    dfm,
                    ["add", src, name],
                )
                assert f"Add {src} as {name}\n" == result.output
            with open(DATABASE_NAME, "rb") as f:
                assert sample_add_data == pickle.load(f)

    def test_duplicate_src(self, runner: CliRunner, sample_add_data):
        with runner.isolated_filesystem():
            runner.invoke(
                dfm,
                ["add", sample_add_data[0][0], sample_add_data[0][1]],
            )
            result = runner.invoke(
                dfm,
                ["add", sample_add_data[0][0], sample_add_data[1][1]],
            )
            assert 2 == result.exit_code

    def test_duplicate_name(self, runner: CliRunner, sample_add_data):
        with runner.isolated_filesystem():
            runner.invoke(
                dfm,
                ["add", sample_add_data[0][0], sample_add_data[0][1]],
            )
            result = runner.invoke(
                dfm,
                ["add", sample_add_data[1][0], sample_add_data[0][1]],
            )
            assert 2 == result.exit_code


class TestShow:
    def test_empty_data(self, runner):
        result = runner.invoke(dfm, ["show"])
        assert "Empty data.\n" == result.output

    def test_populated_data(self, runner, sample_add_data):
        with runner.isolated_filesystem():
            with open(DATABASE_NAME, "wb+") as f:
                pickle.dump(sample_add_data, f)
            result = runner.invoke(dfm, ["show"])
            output = result.output.split("\n")
            assert "/.config/fish.config fish" == output[0]
            assert "/.config/.gitconfig  git" == output[1]
            assert "/.config/rofi.rasi   rofi" == output[2]
