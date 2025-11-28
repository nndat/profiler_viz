import pstats
import io
import sys
import os
import json


def view_profile_html(prof_file_path, output_html_path=None):
    """
    Convert cProfile .prof file to HTML format

    Args:
        prof_file_path: Path to .prof file
        output_html_path: Path to save HTML output (optional, defaults to prof_file_path.html)
    """
    if output_html_path is None:
        output_html_path = prof_file_path.replace('.prof', '.html')

    # Read profile stats
    stats = pstats.Stats(prof_file_path)

    # Parse stats into structured data and calculate summary
    stats_data = []
    call_relationships = {}  # Track caller-callee relationships
    total_functions = 0
    total_primitive_calls = 0
    total_calls = 0
    total_time = 0

    # Find the main/root function (the one with highest cumtime that is not built-in)
    main_function = None
    max_cumtime = 0

    for func, (cc, nc, tt, ct, callers) in stats.stats.items():
        filename, line, func_name = func
        func_key = f"{filename}:{line}({func_name})"

        stats_data.append({
            'ncalls': f"{nc}/{cc}" if nc != cc else str(nc),
            'tottime': tt,
            'percall_tot': tt / nc if nc > 0 else 0,
            'cumtime': ct,
            'percall_cum': ct / cc if cc > 0 else 0,
            'filename': func_key,
            'func_name': func_name,
            'file': filename,
            'line': line
        })

        # Build call relationships (who calls this function, and who this function calls)
        call_relationships[func_key] = {
            'callers': [],
            'callees': []
        }

        # Store callers
        for caller_func, caller_data in callers.items():
            caller_filename, caller_line, caller_name = caller_func
            caller_key = f"{caller_filename}:{caller_line}({caller_name})"
            call_relationships[func_key]['callers'].append({
                'name': caller_key,
                'ncalls': caller_data[0],
                'tottime': caller_data[2],
                'cumtime': caller_data[3]
            })

        total_functions += 1
        total_primitive_calls += cc
        total_calls += nc
        total_time += tt

        # Track the function with highest cumtime (likely the profiled function)
        # Skip built-in functions
        if ct > max_cumtime and not filename.startswith('<'):
            max_cumtime = ct
            main_function = func_name

    # Build callees (reverse of callers)
    for func_key, relationships in call_relationships.items():
        for caller_info in relationships['callers']:
            caller_key = caller_info['name']
            if caller_key in call_relationships:
                call_relationships[caller_key]['callees'].append({
                    'name': func_key,
                    'ncalls': caller_info['ncalls'],
                    'tottime': caller_info['tottime'],
                    'cumtime': caller_info['cumtime']
                })

    # Get total time from stats
    if hasattr(stats, 'total_tt'):
        total_execution_time = stats.total_tt
    else:
        # Calculate from stats
        total_execution_time = total_time

    # Get caller/callee information
    string_buffer = io.StringIO()
    stats.stream = string_buffer
    stats.print_callers(10)
    caller_stats = string_buffer.getvalue()

    # Convert stats_data to JSON for JavaScript
    stats_json = json.dumps(stats_data)
    call_relationships_json = json.dumps(call_relationships)

    # Read template file
    template_path = os.path.join(os.path.dirname(__file__), 'profile_template.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # Replace placeholders in template
    html_content = template.replace('{{prof_file_path}}', prof_file_path)
    html_content = html_content.replace('{{main_function}}', main_function if main_function else 'Unknown')
    html_content = html_content.replace('{{total_functions}}', f"{total_functions:,}")
    html_content = html_content.replace('{{total_calls}}', f"{total_calls:,}")
    html_content = html_content.replace('{{total_primitive_calls}}', f"{total_primitive_calls:,}")
    html_content = html_content.replace('{{total_execution_time}}', f"{total_execution_time:.6f}")
    html_content = html_content.replace('{{caller_stats}}', caller_stats)
    html_content = html_content.replace('{{stats_json}}', stats_json)
    html_content = html_content.replace('{{call_relationships_json}}', call_relationships_json)

    # Write HTML file
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"HTML profile saved to: {output_html_path}")
    return output_html_path


if __name__ == "__main__":
    # Example usage
    prof_file = sys.argv[1]  # Get .prof file path from command line argument
    view_profile_html(prof_file)
