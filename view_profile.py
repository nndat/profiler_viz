import pstats
from pstats import SortKey
import io


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
    total_functions = 0
    total_primitive_calls = 0
    total_calls = 0
    total_time = 0

    # Find the main/root function (the one with highest cumtime that is not built-in)
    main_function = None
    max_cumtime = 0

    for func, (cc, nc, tt, ct, callers) in stats.stats.items():
        filename, line, func_name = func
        stats_data.append({
            'ncalls': f"{nc}/{cc}" if nc != cc else str(nc),
            'tottime': tt,
            'percall_tot': tt / nc if nc > 0 else 0,
            'cumtime': ct,
            'percall_cum': ct / cc if cc > 0 else 0,
            'filename': f"{filename}:{line}({func_name})"
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
    import json
    stats_json = json.dumps(stats_data)

    # Create HTML
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Profile Results - {prof_file_path}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{
            color: #333;
        }}
        h2 {{
            color: #666;
            margin-top: 30px;
            border-bottom: 2px solid #ddd;
            padding-bottom: 5px;
        }}
        .stats-section {{
            background-color: white;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow-x: auto;
        }}
        .file-info {{
            background-color: #e3f2fd;
            padding: 10px;
            border-left: 4px solid #2196F3;
            margin-bottom: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-family: 'Courier New', monospace;
            font-size: 12px;
        }}
        th {{
            background-color: #2196F3;
            color: white;
            padding: 10px;
            text-align: left;
            cursor: pointer;
            user-select: none;
            position: sticky;
            top: 0;
        }}
        th:hover {{
            background-color: #1976D2;
        }}
        th.sortable::after {{
            content: ' ⇅';
            opacity: 0.5;
        }}
        th.sort-asc::after {{
            content: ' ↑';
            opacity: 1;
        }}
        th.sort-desc::after {{
            content: ' ↓';
            opacity: 1;
        }}
        td {{
            padding: 8px;
            border-bottom: 1px solid #ddd;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .num {{
            text-align: right;
        }}
        .filter-box {{
            margin-bottom: 15px;
        }}
        .filter-box input {{
            padding: 8px;
            width: 100%;
            max-width: 500px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }}
        pre {{
            white-space: pre;
            margin: 0;
            font-size: 12px;
            line-height: 1.4;
        }}
    </style>
</head>
<body>
    <h1>Python Profile Results</h1>

    <div class="file-info">
        <strong>Profiled Function:</strong> {main_function if main_function else 'Unknown'}<br>
        <strong>Profile file:</strong> {prof_file_path}
    </div>

    <div class="stats-section">
        <h2>Overview</h2>
        <table style="width: auto; margin-bottom: 20px;">
            <tr>
                <td style="padding: 8px; font-weight: bold; border: none;">Total Functions:</td>
                <td style="padding: 8px; border: none;">{total_functions:,}</td>
            </tr>
            <tr>
                <td style="padding: 8px; font-weight: bold; border: none;">Total Function Calls:</td>
                <td style="padding: 8px; border: none;">{total_calls:,}</td>
            </tr>
            <tr>
                <td style="padding: 8px; font-weight: bold; border: none;">Primitive Calls:</td>
                <td style="padding: 8px; border: none;">{total_primitive_calls:,}</td>
            </tr>
            <tr>
                <td style="padding: 8px; font-weight: bold; border: none;">Total Execution Time:</td>
                <td style="padding: 8px; border: none;">{total_execution_time:.6f} seconds</td>
            </tr>
        </table>
    </div>

    <div class="stats-section">
        <h2>Profile Statistics (Sortable)</h2>
        <div class="filter-box">
            <input type="text" id="filterInput" placeholder="Filter by function name or file path...">
        </div>
        <table id="statsTable">
            <thead>
                <tr>
                    <th class="sortable" data-column="ncalls" data-type="text">ncalls</th>
                    <th class="sortable" data-column="tottime" data-type="number">tottime</th>
                    <th class="sortable" data-column="percall_tot" data-type="number">percall</th>
                    <th class="sortable" data-column="cumtime" data-type="number">cumtime</th>
                    <th class="sortable" data-column="percall_cum" data-type="number">percall</th>
                    <th class="sortable" data-column="filename" data-type="text">filename:lineno(function)</th>
                </tr>
            </thead>
            <tbody id="statsBody">
            </tbody>
        </table>
    </div>

    <div class="stats-section">
        <h2>Caller Statistics (Top 10)</h2>
        <pre>{caller_stats}</pre>
    </div>

    <div class="stats-section">
        <h2>Column Descriptions</h2>
        <pre>
ncalls  - number of calls
tottime - total time spent in the function (excluding sub-functions)
percall - tottime divided by ncalls
cumtime - cumulative time spent in the function (including sub-functions)
percall - cumtime divided by primitive calls
filename:lineno(function) - location and name of the function
        </pre>
    </div>

    <script>
        // Stats data
        const statsData = {stats_json};
        let currentSort = {{ column: 'cumtime', direction: 'desc' }};
        let filteredData = [...statsData];

        // Render table
        function renderTable(data) {{
            const tbody = document.getElementById('statsBody');
            tbody.innerHTML = '';

            data.forEach(row => {{
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td class="num">${{row.ncalls}}</td>
                    <td class="num">${{row.tottime.toFixed(6)}}</td>
                    <td class="num">${{row.percall_tot.toFixed(6)}}</td>
                    <td class="num">${{row.cumtime.toFixed(6)}}</td>
                    <td class="num">${{row.percall_cum.toFixed(6)}}</td>
                    <td>${{row.filename}}</td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        // Sort data
        function sortData(column, type, forceDirection = null) {{
            let direction;
            if (forceDirection) {{
                direction = forceDirection;
            }} else {{
                direction = currentSort.column === column && currentSort.direction === 'desc' ? 'asc' : 'desc';
            }}
            currentSort = {{ column, direction }};

            filteredData.sort((a, b) => {{
                let valA = a[column];
                let valB = b[column];

                if (type === 'number') {{
                    valA = parseFloat(valA);
                    valB = parseFloat(valB);
                }}

                if (direction === 'asc') {{
                    return valA > valB ? 1 : valA < valB ? -1 : 0;
                }} else {{
                    return valA < valB ? 1 : valA > valB ? -1 : 0;
                }}
            }});

            updateSortIndicators(column, direction);
            renderTable(filteredData);
        }}

        // Update sort indicators
        function updateSortIndicators(column, direction) {{
            document.querySelectorAll('th').forEach(th => {{
                th.classList.remove('sort-asc', 'sort-desc');
            }});
            const header = document.querySelector(`th[data-column="${{column}}"]`);
            if (header) {{
                header.classList.add(`sort-${{direction}}`);
            }}
        }}

        // Filter data
        function filterData(searchTerm) {{
            searchTerm = searchTerm.toLowerCase();
            filteredData = statsData.filter(row =>
                row.filename.toLowerCase().includes(searchTerm)
            );
            sortData(currentSort.column, document.querySelector(`th[data-column="${{currentSort.column}}"]`).dataset.type);
        }}

        // Event listeners
        document.querySelectorAll('th.sortable').forEach(th => {{
            th.addEventListener('click', () => {{
                sortData(th.dataset.column, th.dataset.type);
            }});
        }});

        document.getElementById('filterInput').addEventListener('input', (e) => {{
            filterData(e.target.value);
        }});

        // Initial render (sorted by cumtime desc)
        sortData('cumtime', 'number', 'desc');
    </script>
</body>
</html>"""

    # Write HTML file
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"HTML profile saved to: {output_html_path}")
    return output_html_path


if __name__ == "__main__":
    # Example usage
    prof_file = "profile_20251128145255.prof"
    view_profile_html(prof_file)
