document.addEventListener('DOMContentLoaded', function () {
  const searchInput = document.getElementById('searchInput');
  const foroTableBody = document.getElementById('foroTableBody');
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  const tableInfo = document.getElementById('tableInfo');

  let currentPage = 1;
  const rowsPerPage = 5;

  function filterTable() {
      const filter = searchInput.value.toLowerCase();
      const rows = foroTableBody.getElementsByTagName('tr');
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
      currentPage = 1;
      updateTable();
  }

  function updateTable() {
      const rows = foroTableBody.getElementsByTagName('tr');
      let totalRows = 0;
      for (let i = 0; i < rows.length; i++) {
          if (rows[i].getAttribute('data-visible') !== 'false') {
              totalRows++;
          }
      }
      const start = (currentPage - 1) * rowsPerPage;
      const end = start + rowsPerPage;
      let visibleRows = 0;
      for (let i = 0; i < rows.length; i++) {
          if (rows[i].getAttribute('data-visible') !== 'false') {
              if (visibleRows >= start && visibleRows < end) {
                  rows[i].style.display = '';
              } else {
                  rows[i].style.display = 'none';
              }
              visibleRows++;
          } else {
              rows[i].style.display = 'none';
          }
      }
      tableInfo.innerHTML = `Mostrando <b>${Math.min(start + 1, totalRows)}-${Math.min(end, totalRows)}</b> de ${totalRows}`;
      prevBtn.disabled = currentPage === 1;
      nextBtn.disabled = end >= totalRows;
  }

  searchInput.addEventListener('input', filterTable);

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

  // Inicializar la tabla
  filterTable();
});