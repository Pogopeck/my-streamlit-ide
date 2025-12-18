import streamlit as st
import sys
from io import StringIO
import contextlib

st.title("🐍 Simple Python Code Runner (Streamlit IDE)")

# Use a safer approach: restrict what can be done
code = st.text_area(
    "Enter Python code (read-only demo – no file/network access):",
    value='print("Hello from Streamlit IDE!")\nfor i in range(3):\n    print(f"Line {i}")',
    height=200
)

if st.button("▶️ Run Code"):
    if code.strip():
        # Capture stdout
        @contextlib.contextmanager
        def capture_stdout():
            old = sys.stdout
            out = StringIO()
            try:
                sys.stdout = out
                yield out
            finally:
                sys.stdout = old

        try:
            # ⚠️ NEVER use exec() with untrusted input in real apps!
            # This is for demo only.
            with capture_stdout() as output:
                exec(code, {"__builtins__": {}})  # severely restricted globals
            result = output.getvalue()
            st.subheader("Output:")
            st.code(result, language="text")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter some code.")
