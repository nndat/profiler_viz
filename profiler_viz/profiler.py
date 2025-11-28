import cProfile
from datetime import datetime
import os
from .viewer import view_profile_html


def func_profile(dest=None):
    """
    Decorator to profile a function and generate HTML report

    Args:
        dest: Directory to save profile and HTML files (optional, defaults to current directory)

    Usage:
        @func_profile()
        def my_function():
            pass

        @func_profile(dest="/path/to/output")
        def my_function():
            pass
    """
    def decorator_wrapper(func):
        # Flag to prevent profiling recursive calls
        _is_profiling = False

        def decorator(*args, **kwargs):
            nonlocal _is_profiling

            # If already profiling, just call the function without profiling again
            if _is_profiling:
                return func(*args, **kwargs)

            # Set flag to indicate we're profiling
            _is_profiling = True

            try:
                # Determine output directory
                output_dir = dest if dest else os.getcwd()
                os.makedirs(output_dir, exist_ok=True)

                # Generate timestamp
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

                # Create file paths with function name
                func_name = func.__name__
                prof_filename = f"{func_name}_{timestamp}.prof"
                html_filename = f"{func_name}_{timestamp}.html"

                prof_path = os.path.join(output_dir, prof_filename)
                html_path = os.path.join(output_dir, html_filename)

                # Profile the function
                profile = cProfile.Profile()
                result = profile.runcall(func, *args, **kwargs)
                profile.dump_stats(prof_path)

                # Generate HTML report
                try:
                    view_profile_html(prof_path, html_path)
                    print(f"Profile saved to: {prof_path}")
                    print(f"HTML report saved to: {html_path}")
                except Exception as e:
                    print(f"Error generating HTML report: {e}")

                return result
            finally:
                # Reset flag after profiling is done
                _is_profiling = False

        return decorator

    return decorator_wrapper

