import great_expectations as gx
import pathlib

context_root_dir = pathlib.Path("C:/Users/riley/modern-data-eng/dags/include/gx").as_posix()
context = gx.get_context(context_root_dir=context_root_dir)

# datasource_name = "aggregated_data"
# path_to_folder_containing_csv_files = "data/"

# datasource = context.sources.add_or_update_pandas_filesystem(
#     name=datasource_name, base_directory=path_to_folder_containing_csv_files
# )

# asset_name = "aggregated_data_asset"
# batching_regex = r".*\.csv"
# datasource.add_csv_asset(name=asset_name, batching_regex=batching_regex)

# # Render data docs
# context.build_data_docs()

data_asset = context.get_datasource("aggregated_data").get_asset("aggregated_data_asset")
batch_request = data_asset.build_batch_request()

checkpoint = context.add_or_update_checkpoint(
    name="aggregate_data_checkpoint",
    validations=[
        {
            "batch_request": batch_request,
            "expectation_suite_name": "page_view_suite",
        },
    ],
)