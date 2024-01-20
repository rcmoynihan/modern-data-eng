import os

import logging

logger = logging.getLogger(__file__)

logger.error("test error log")

# from opentelemetry import trace

# tracer = trace.get_tracer_provider().get_tracer(__name__)

# # Trace context correlation
# with tracer.start_as_current_span("foo"):
#     # Do something
#     current_span = trace.get_current_span()
#     current_span.add_event("This is a span event")
#     logging.getLogger().error("This is a log message")
