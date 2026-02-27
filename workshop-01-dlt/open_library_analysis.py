import marimo

__generated_with = "0.20.2"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import dlt
    import altair as alt
    import pandas as pd
    import duckdb

    return alt, duckdb, mo


@app.cell
def _(duckdb):
    # Connect to the DuckDB database
    # The database path is local to the workshop-01-dlt directory
    con = duckdb.connect("open_library_pipeline.duckdb", read_only=True)
    return (con,)


@app.cell
def _(mo):
    mo.md("""
    # Open Library Data Analysis
    """)
    return


@app.cell
def _(con):
    # Query for books per author
    # We join books with books__author_name
    authors_df = con.execute("""
        SELECT 
            an.value AS author_name, 
            COUNT(b._dlt_id) AS book_count
        FROM open_library_data_20260227023442.books b
        JOIN open_library_data_20260227023442.books__author_name an ON b._dlt_id = an._dlt_parent_id
        GROUP BY author_name
        ORDER BY book_count DESC
        LIMIT 20
    """).df()
    return (authors_df,)


@app.cell
def _(alt, authors_df, mo):
    # Create bar chart for books per author
    author_chart = alt.Chart(authors_df).mark_bar().encode(
        x=alt.X('book_count:Q', title='Number of Books'),
        y=alt.Y('author_name:N', sort='-x', title='Author Name'),
        tooltip=['author_name', 'book_count']
    ).properties(
        title='Top 20 Authors by Number of Books',
        width=600,
        height=400
    )

    mo.hstack([mo.ui.table(authors_df), author_chart])
    return


@app.cell
def _(con):
    # Query for books over time (first_publish_year)
    # We filter out nulls and group by year
    timeline_df = con.execute("""
        SELECT 
            first_publish_year, 
            COUNT(*) AS book_count
        FROM open_library_data_20260227023442.books
        WHERE first_publish_year IS NOT NULL
        GROUP BY first_publish_year
        ORDER BY first_publish_year
    """).df()
    return (timeline_df,)


@app.cell
def _(alt, mo, timeline_df):
    # Create line chart for books over time
    timeline_chart = alt.Chart(timeline_df).mark_line(point=True).encode(
        x=alt.X('first_publish_year:O', title='First Publish Year'),
        y=alt.Y('book_count:Q', title='Number of Books'),
        tooltip=['first_publish_year', 'book_count']
    ).properties(
        title='Number of Books Over Time',
        width=800,
        height=400
    )

    mo.vstack([mo.md("### Books Published Over Time"), timeline_chart])
    return


if __name__ == "__main__":
    app.run()
