const { board } = window.miro;

async function init() {
  await board.ui.on("icon:click", async () => {
    await board.ui.openPanel({ pageUrl: "app.html" });
  });
}

init();

// const { board } = window.miro;

// async function init() {
//   await board.ui.on("icon:click", async () => {
//     const stickyNote = await board.createStickyNote({
//       content: "Hello, MAD!",
//     });

//     await board.viewport.zoomTo(stickyNote);
//   });
// }

// init();
