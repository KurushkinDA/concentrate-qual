import React, { useState, useRef, useEffect } from 'react';
import jspreadsheet from 'jspreadsheet-ce';
import { useNavigate } from 'react-router-dom';
import 'jspreadsheet-ce/dist/jspreadsheet.css';
import Header from '../components/Header';
import { apiFetch } from '../api';
export default function Home() {

  const tableRef = useRef(null);
  const [spreadsheetLoaded, setSpreadsheetLoaded] = useState(false);
  const [records, setRecords] = useState([]);
  const [error, setError] = useState(null);
  const [selectedMonth, setSelectedMonth] = useState('');

  useEffect(() => {
    fetchRecords();
  }, []);

  const navigate = useNavigate();
  const fetchRecords = async (month = null) => {
    try {
      const query = month ? `?report_month=${month}` : '';
      const res = await apiFetch(`/concentrates${query}`, null, 'GET');
      setRecords(res.items || []);
    } catch (err) {
      if (err.message === '401') {
        navigate('/login');
      } else {
        setError('Ошибка загрузки данных');
      }
    }
  };




  return (
    <>
    <Header />
        <main className="p-6">
            <h1 className="text-2xl font-bold mb-4">Показатели концентрата</h1>
            <div className="flex items-center gap-4 mb-4">
            <input
                type="month"
                className="border px-3 py-2 rounded"
                value={selectedMonth}
                onChange={(e) => setSelectedMonth(e.target.value)}
            />
            <button
                onClick={() => fetchRecords(selectedMonth)}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
                Применить
            </button>
            </div>
            <div className="overflow-x-auto">
                <table className="min-w-full border text-sm">
                    <thead>
                    <tr className="bg-gray-200">
                        <th className="border px-4 py-2">Наименование</th>
                        <th className="border px-4 py-2">Железо</th>
                        <th className="border px-4 py-2">Кремний</th>
                        <th className="border px-4 py-2">Алюминий</th>
                        <th className="border px-4 py-2">Кальций</th>
                        <th className="border px-4 py-2">Сера</th>
                        <th className="border px-4 py-2">Месяц</th>
                        <th className="border px-4 py-2">Пользователь</th>
                    </tr>
                    </thead>
                    <tbody>
                    {records.map((rec) => (
                        <tr key={rec.id}>
                        <td className="border px-4 py-2">{rec.name}</td>
                        <td className="border px-4 py-2">{rec.iron}</td>
                        <td className="border px-4 py-2">{rec.silicon}</td>
                        <td className="border px-4 py-2">{rec.aluminum}</td>
                        <td className="border px-4 py-2">{rec.calcium}</td>
                        <td className="border px-4 py-2">{rec.sulfur}</td>
                        <td className="border px-4 py-2">{rec.report_month}</td>
                        <td className="border px-4 py-2">{rec.user?.username || ''}</td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        </main>
    </>
  );
}