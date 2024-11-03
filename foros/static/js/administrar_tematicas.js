document.addEventListener('DOMContentLoaded', function () {
  const deleteButtons = document.querySelectorAll('.delete-tematica-btn');
  const deleteModal = document.getElementById('deleteModal');
  const cancelButton = document.getElementById('cancelButton');
  const confirmDeleteButton = document.getElementById('confirmDeleteButton');
  let currentDeleteUrl = '';

  deleteButtons.forEach(button => {
    button.addEventListener('click', (event) => {
      event.preventDefault();
      currentDeleteUrl = button.getAttribute('data-url');
      deleteModal.classList.remove('hidden');
    });
  });

  cancelButton.addEventListener('click', () => {
    deleteModal.classList.add('hidden');
  });

  confirmDeleteButton.addEventListener('click', () => {
    window.location.href = currentDeleteUrl;
  });

  window.addEventListener('click', (event) => {
    if (event.target === deleteModal) {
      deleteModal.classList.add('hidden');
    }
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const searchInput = document.getElementById('searchInput');
  const tematicaTableBody = document.getElementById('tematicaTableBody');
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  const tableInfo = document.getElementById('tableInfo');

  let currentPage = 1;
  const rowsPerPage = 5;

  function filterTable() {
    const filter = searchInput.value.toLowerCase();
    const rows = tematicaTableBody.getElementsByTagName('tr');
    for (let i = 0; i < rows.length; i++) {
      const cells = rows[i].getElementsByTagName('td');
      let match = false;
      for (let j = 0; j < cells.length; j++) {
        if (cells[j].innerText.toLowerCase().includes(filter)) {
          match = true;
          break;
        }
      }
      rows[i].setAttribute('data-visible', match ? 'true' : 'false');
    }
  }

  function updateTable() {
    const rows = tematicaTableBody.getElementsByTagName('tr');
    let totalRows = 0;
    for (let i = 0; i < rows.length; i++) {
      if (rows[i].getAttribute('data-visible') === 'true') {
        totalRows++;
      }
    }
    const start = (currentPage - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    let visibleRows = 0;
    for (let i = 0; i < rows.length; i++) {
      if (rows[i].getAttribute('data-visible') === 'true') {
        rows[i].style.display = (visibleRows >= start && visibleRows < end) ? '' : 'none';
        visibleRows++;
      } else {
        rows[i].style.display = 'none';
      }
    }
    tableInfo.innerHTML = `Mostrando <b>${Math.min(start + 1, totalRows)}-${Math.min(end, totalRows)}</b> de ${totalRows}`;
    prevBtn.disabled = currentPage === 1;
    nextBtn.disabled = end >= totalRows;
  }

  searchInput.addEventListener('input', () => {
    currentPage = 1;
    filterTable();
    updateTable();
  });

  prevBtn.addEventListener('click', () => {
    if (currentPage > 1) {
      currentPage--;
      updateTable();
    }
  });

  nextBtn.addEventListener('click', () => {
    currentPage++;
    updateTable();
  });

  filterTable();
  updateTable();
});
