# Profiler Viz

A beautiful Python profiler with interactive HTML visualization. Profile your Python functions and get stunning visual reports with charts, sortable tables, and call tree analysis.

## Features

✨ **Beautiful HTML Reports** - Interactive visualizations with charts and graphs

📊 **Performance Charts** - See top functions by time and call count at a glance

🔍 **Sortable Statistics** - Click column headers to sort by any metric

🌳 **Call Tree Analysis** - Click any function to see its callers and callees

🎯 **Easy to Use** - Just add a decorator to your function

## Installation

```bash
pip install profiler-viz
```

Or install from source:

```bash
git clone https://github.com/yourusername/profiler-viz.git
cd profiler-viz
pip install -e .
```

## Quick Start

### Basic Usage

```python
from profiler_viz import func_profile

@func_profile()
def my_function():
    # Your code here
    result = sum(range(1000000))
    return result

# Run your function
my_function()
```

This will automatically:
- Profile the function execution
- Generate a `.prof` file
- Create a beautiful HTML report
- Both files named: `my_function_YYYYMMDDHHmmss.{prof,html}`

### Custom Output Directory

```python
from profiler_viz import func_profile

@func_profile(dest="./profiling_results")
def process_data():
    # Your code here
    pass

process_data()
```

### Convert Existing .prof Files

```python
from profiler_viz import view_profile_html

# Convert a .prof file to HTML
view_profile_html("my_profile.prof")

# Or specify output path
view_profile_html("my_profile.prof", "report.html")
```

Or use the command line:

```bash
profiler-viz my_profile.prof
```

## HTML Report Features

The generated HTML report includes:

### 📈 Overview Section
- Total functions profiled
- Total function calls
- Primitive calls
- Total execution time

### 📊 Performance Charts
1. **Top 10 Functions by Cumulative Time** - Functions that take the most time including their callees
2. **Top 10 Functions by Total Time** - Functions that take the most time excluding callees
3. **Top 10 Most Called Functions** - Functions called most frequently
4. **Time Distribution Pie Chart** - Visual breakdown of where time is spent

### 📋 Sortable Statistics Table
- Click any column header to sort
- Filter functions by name or file path
- View detailed metrics:
  - `ncalls` - Number of calls
  - `tottime` - Total time in function (excluding sub-functions)
  - `percall` - Time per call
  - `cumtime` - Cumulative time (including sub-functions)
  - `filename:lineno(function)` - Location and name

### 🌳 Call Tree Modal
- Click any row to see:
  - Who calls this function (callers)
  - What this function calls (callees)
  - Call counts and timing for each relationship

## Examples

### Example 1: Profile a Recursive Function

```python
from profiler_viz import func_profile

@func_profile()
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = fibonacci(20)
```

### Example 2: Profile Data Processing

```python
from profiler_viz import func_profile
import pandas as pd

@func_profile(dest="./analysis_reports")
def analyze_data(filename):
    df = pd.read_csv(filename)
    # Complex data processing
    result = df.groupby('category').agg({
        'value': ['sum', 'mean', 'std']
    })
    return result

analyze_data("large_dataset.csv")
```

### Example 3: Profile with Custom Logic

```python
from profiler_viz import func_profile

@func_profile(dest="./benchmarks")
def benchmark_algorithm(data_size):
    data = list(range(data_size))
    # Test different sorting approaches
    sorted_data = sorted(data, reverse=True)
    return sorted_data

# Run benchmark
benchmark_algorithm(1000000)
```

## Understanding the Output

### File Naming
Files are automatically named using the pattern:
```
<function_name>_YYYYMMDDHHmmss.prof
<function_name>_YYYYMMDDHHmmss.html
```

For example:
```
my_function_20231128143022.prof
my_function_20231128143022.html
```

### Metrics Explained

- **ncalls**: Number of calls. If shown as `X/Y`, Y is primitive calls, X is total calls
- **tottime**: Time spent in this function alone (excluding calls to sub-functions)
- **percall**: Average time per call (`tottime / ncalls`)
- **cumtime**: Total time spent in this function including all sub-functions
- **percall**: Average cumulative time (`cumtime / primitive calls`)

### What to Look For

1. **High cumtime** - Functions that take the most overall time
2. **High tottime** - Functions doing expensive operations themselves
3. **High ncalls** - Functions called many times (candidates for caching/optimization)
4. **High percall** - Individual calls that are slow

## Tips and Best Practices

1. **Start with cumtime** - Sort by cumulative time to find the biggest bottlenecks
2. **Check the call tree** - Click on slow functions to understand the call chain
3. **Look for patterns** - Use the filter box to find related functions
4. **Compare runs** - Profile before and after optimizations to measure impact
5. **Use custom directories** - Organize profiles by feature or test case

## Requirements

- Python 3.7+
- No external dependencies (uses only Python standard library)

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or contributions, please visit:
https://github.com/nndat/profiler_viz/issues
