import sys
import unittest


def main():
    if len(sys.argv) != 2:
        sys.exit('Usage: %s <path_to_sdk>' % sys.argv[0])
    sys.path.insert(0, sys.argv[1])
    import dev_appserver
    dev_appserver.fix_sys_path()
    suite = unittest.loader.TestLoader().discover('.')
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    main()
