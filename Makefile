main_no_weave:
	uv run streamlit run ./src/main_no_weave.py

main_weave_init:
	uv run streamlit run ./src/main_weave_init.py

main_weave_op:
	uv run streamlit run ./src/main_weave_op.py

main_weave_attrs:
	uv run streamlit run ./src/main_weave_attrs.py

main_weave_model:
	uv run streamlit run ./src/main_weave_model.py

main_weave_feedback:
	uv run streamlit run ./src/main_weave_feedback.py

evaluate_app:
	uv run ./src/evaluate.py

start_app:
	uv run streamlit run ./src/main.py