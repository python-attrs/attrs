#!/bin/bash
set -e
case "$1" in
  base)
    pytest tests/ --ignore=tests/test_factory_validation_order.py
    ;;
  new)
    pytest tests/test_factory_validation_order.py
    ;;
  *)
    echo "Usage: ./test.sh {base|new}"
    exit 1
    ;;
esac
