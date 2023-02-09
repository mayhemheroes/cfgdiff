#!/usr/bin/env python3

import atheris
import sys
import fuzz_helpers

with atheris.instrument_imports(include=['cfgdiff', 'json', 'yaml', 'lxml']):
    import cfgdiff

diff_types = [
    cfgdiff.INIDiff,
    cfgdiff.ConfigDiff,
    cfgdiff.JSONDiff,
    cfgdiff.ReconfigureDiff,
    cfgdiff.ZoneDiff,
    cfgdiff.XMLDiff,
    cfgdiff.YAMLDiff,
]


def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    test_ty = fdp.ConsumeIntInRange(0, 7)
    ordered = fdp.ConsumeBool()
    diff_cls = fdp.PickValueInList(diff_types)

    with fdp.ConsumeTemporaryFile('conf', all_data=True, as_bytes=False) as conf_path:
        diff_cls(conf_path, ordered=ordered)

def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
