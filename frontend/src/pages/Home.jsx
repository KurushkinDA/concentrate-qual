import React, { useState, useEffect } from 'react';
import 'jspreadsheet-ce/dist/jspreadsheet.css';
import Header from '../components/Header';
import { apiFetch } from '../api';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';

export default function Home() {
  const [records, setRecords] = useState([]);
  const [selectedMonth, setSelectedMonth] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchRecords();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fetchRecords = async (month = null) => {
    try {
      const query = month ? `?report_month=${month}` : '';
      const res = await apiFetch(`/concentrates${query}`, null, 'GET');
      setRecords(res.items || []);
    } catch (err) {
      if (err.status === 401) {
        toast.error('Сессия истекла. Войдите заново.');
        navigate('/login');
      } else {
        toast.error('Ошибка загрузки данных', {
          description: err.message || 'Неизвестная ошибка',
        });
        setError('Ошибка загрузки данных');
      }
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Вы уверены, что хотите удалить запись?')) return;

    try {
      await apiFetch(`/concentrates/${id}`, null, 'DELETE');
      toast.success('Запись удалена');
      fetchRecords(selectedMonth);
    } catch (err) {
      if (err.status === 401) {
        toast.error('Сессия истекла');
        navigate('/login');
      } else {
        toast.error('Ошибка удаления', {
          description: err.message || 'Неизвестная ошибка',
        });
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
                <th className="border px-4 py-2">Действие</th>
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
                  <td className="border px-4 py-2 text-center">
                    <button
                      onClick={() => handleDelete(rec.id)}
                      className="text-red-600 hover:underline"
                    >
                      Удалить
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
    </>
  );
}