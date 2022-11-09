function deleteNote(noteId) {
  fetch("/delete_resume", {
    method: "POST",
    body: JSON.stringify({noteId: noteId}),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function deleteItem(itemId) {
  fetch("/delete_item", {
    method: "POST",
    body: JSON.stringify({itemId: itemId}),
  }).then((_res) => {
    window.location.href = "/";
  });
}