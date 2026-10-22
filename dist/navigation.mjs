// Preserve the selected evidence route when the keyboard skip link is activated.
export function bindSkipLink(link, main) {
  link.addEventListener("click", (event) => {
    event.preventDefault();
    main.focus();
  });
}
