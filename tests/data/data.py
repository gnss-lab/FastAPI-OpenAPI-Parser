test_data = [
    ("/rinex_to_csv/upload_rinex", {
        "auto_generate_enabled": False,
        "large_file_enabled": False,
        "large_file_queues": False,
        "get_body_multipart_form_data": ['rinex'],
        "get_body_application_json": None,
        "get_queries_param": (['rinex_to_csv_processing_id'], [False], [True])
    }),
    ("/rinex_to_csv/upload_nav", {
        "auto_generate_enabled": True,
        "large_file_enabled": False,
        "large_file_queues": False,
        "get_body_multipart_form_data": ['rinex'],
        "get_body_application_json": None,
        "get_queries_param": (['url', 'rinex_to_csv_processing_id'], [True, False], [False, True])
    }),
    ("/rinex_to_csv/run", {
        "auto_generate_enabled": False,
        "large_file_enabled": True,
        "large_file_queues": ["test1", "test2"],
        "get_body_multipart_form_data": None,
        "get_body_application_json": ['ConversionParams'],
        "get_queries_param": (['rinex_to_csv_processing_id'], [False], [True])
    }),
    ("/rinex_to_csv/get_result", {
        "auto_generate_enabled": False,
        "large_file_enabled": False,
        "large_file_queues": False,
        "get_body_multipart_form_data": None,
        "get_body_application_json": None,
        "get_queries_param": (None, None, None)
    })
]