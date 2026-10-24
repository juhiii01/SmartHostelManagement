document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".click-row").forEach(row => {
    row.addEventListener("click", () => {
      const url = row.dataset.href;
      if (url) window.location.href = url;
    });
  });
  const locationSelect = document.querySelector('select[name="location"]');
  const roomInput = document.querySelector('input[name="room_number"]');
  if (locationSelect && roomInput) {
    const roomField = roomInput.closest(".field");
    const updateRoom = () => {
      const isRoom = locationSelect.value === "Hostel Room";
      roomField.style.display = isRoom ? "block" : "none";
      if (!isRoom) roomInput.value = "";
    };
    locationSelect.addEventListener("change", updateRoom);
    updateRoom();
  }
});
