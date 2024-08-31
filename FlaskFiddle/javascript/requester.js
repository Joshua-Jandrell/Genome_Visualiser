const HREF = "http://127.0.0.1:5000"

function getMatrix(form){
    matrix_data = {
        rows: form.rows.value,
        cols: form.cols.value
      };
    console.log(matrix_data);
    document.getElementById("start-msg").textContent = "Getting matrix...";
    FetchServer(matrix_data,"/matrix").then((response) => {
      //console.log("log made\n" + response);
    });
}

function FetchServer(input, path) {
  return new Promise((resolve) => {
    fetch(serverHref + path, {
      method: "POST",
      headers: {
        "Content-type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(input),
    })
      .then((resposne) => {
        return resposne.json();
      })
      .then((json) => {
        resolve(json);
      });
  });
}