import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

const TableEditor = () => {
  const [rows, setRows] = useState(2);
  const [cols, setCols] = useState(2);
  const [tableData, setTableData] = useState(
    Array.from({ length: rows }, () => Array(cols).fill(''))
  );
  const [resultData, setResultData] = useState([]);
  const [alpha, setAlpha] = useState(0.5);


  const addRow = () => {
    setRows(rows + 1);
    setTableData([...tableData, Array(cols).fill('')]);
  };

  const addColumn = () => {
    setCols(cols + 1);
    setTableData(tableData.map(row => [...row, '']));
  };

  const deleteRow = (index) => {
    setRows(rows - 1);
    setTableData(tableData.filter((_, i) => i !== index));
  };

  const deleteColumn = (index) => {
    setCols(cols - 1);
    setTableData(tableData.map(row => row.filter((_, i) => i !== index)));
  };

  const handleCellChange = (rowIndex, colIndex, value) => {
    const updatedTableData = [...tableData];
    updatedTableData[rowIndex][colIndex] = value;
    setTableData(updatedTableData);
  };

  const handleAlphaChange = (e) => {
    setAlpha(parseFloat(e.target.value));
  };

  const writeTableData = async () => {
    try {
      const response = await fetch('https://boltzman.pythonanywhere.com/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({tableData, alpha}),
      });

      if (response.ok) {
        const result = await response.json();
        setResultData(result);
      } else {
        window.alert('Failed to send table data');
      }
    } catch (error) {
      console.log(error)
      window.alert('Error:', error);
    }
  };

  return (
    <div className="container mt-4">
      <h1>Decision Table</h1>
      <button className="btn btn-success mr-2" onClick={writeTableData}>
        Write Table Data
      </button>
      <button className="btn btn-primary mr-2" onClick={addRow}>
        Add Row
      </button>
      <button className="btn btn-primary mr-2" onClick={addColumn}>
        Add Column
      </button>
      <div className="mb-3">
        <label htmlFor="alphaInput" className="form-label">
          Alpha Value:
        </label>
        <input
          type="number"
          step="0.01"
          min="0"
          max="1"
          className="form-control"
          id="alphaInput"
          value={alpha}
          onChange={handleAlphaChange}
        />
      </div>
      <table className="table table-bordered">
        <tbody>
          {tableData.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {row.map((cell, colIndex) => (
                <td key={colIndex}>
                  <input
                    type="text"
                    className="form-control"
                    value={cell}
                    onChange={(e) =>
                      handleCellChange(rowIndex, colIndex, e.target.value)
                    }
                  />
                </td>
              ))}
              <td>
                <button
                  className="btn btn-danger btn-sm"
                  onClick={() => deleteRow(rowIndex)}
                >
                  Delete Row
                </button>
              </td>
            </tr>
          ))}
          <tr>
            {Array.from({ length: cols }, (_, colIndex) => (
              <td key={colIndex}>
                <button
                  className="btn btn-danger btn-sm"
                  onClick={() => deleteColumn(colIndex)}
                >
                  Delete Column
                </button>
              </td>
            ))}
          </tr>
        </tbody>
      </table>
      <div>
        <h2>Results:</h2>
        <ul>
          {Object.entries(resultData).map(([criteria, value]) => (
            <li key={criteria}>
              <strong>{criteria}:</strong> {value}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default TableEditor;
