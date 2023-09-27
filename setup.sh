mkdir -р ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
 " > ~/.streamLit/config.toml
