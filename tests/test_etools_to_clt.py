from pathlib import Path
from os import environ
from cwl_utils.etools_to_clt import traverse
import cwl_utils.parser_v1_0 as parser
from cwltool.errors import WorkflowException
from pytest import raises

HERE = Path(__file__).resolve().parent


def test_workflow_top_level_format_expr(tmp_path):
    with raises(WorkflowException, match=r".*format specification.*"):
        result, modified = traverse(parser.load_document(str(HERE/"../testdata/workflow_input_format_expr.cwl")))

def test_workflow_top_level_sf_expr(tmp_path):
    with raises(WorkflowException, match=r".*secondaryFiles.*"):
        result, modified = traverse(parser.load_document(str(HERE/"../testdata/workflow_input_sf_expr.cwl")))

def test_workflow_top_level_sf_expr_array(tmp_path):
    with raises(WorkflowException, match=r".*secondaryFiles.*"):
        result, modified = traverse(parser.load_document(str(HERE/"../testdata/workflow_input_sf_expr_array.cwl")))


