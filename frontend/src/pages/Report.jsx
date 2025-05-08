import React, { useState } from 'react';
import Header from '../components/Header';
import { apiFetch } from '../api';
import { toast } from 'sonner';
import { useNavigate } from 'react-router-dom';

const LABELS_RU = {
  average_iron: 'Среднее железо',
  min_iron: 'Мин. железо',
  max_iron: 'Макс. железо',

  average_silicon: 'Средний кремний',
  min_silicon: 'Мин. кремний',
  max_silicon: 'Макс. кремний',

  average_aluminum: 'Средний алюминий',
  min_aluminum: 'Мин. алюминий',
  max_aluminum: 'Макс. алюминий',

  average_calcium: 'Средний кальций',
  min_calcium: 'Мин. кальций',
  max_calcium: 'Макс. кальций',

  average_sulfur: 'Средняя сера',
  min_sulfur: 'Мин. сера',
  max_sulfur: 'Макс. сера',
};

export default function ReportPage() {
  const [month, setMonth] = useState('');
  const [data, setData] = useState(null);
  const navigate = useNavigate();

  const fetchReport = async () => {
    if (!month) {
      toast.error('Выберите месяц');
      return;
    }

    try {
      const res = await apiFetch(`/concentrates/report?report_month=${month}`, null, 'GET');
      setData(res.data);
      toast.success(res.message || 'Отчёт получен');
    } catch (err) {
      if (err.status === 401) {
        toast.error('Сессия истекла. Пожалуйста, войдите заново.');
        navigate('/login');
      } else {
        toast.error('Ошибка загрузки отчёта', { description: err.message });
      }
    }
  };

  return (
    <>
      <Header />
      <main className="p-6">
        <h1 className="text-2xl font-bold mb-4">Отчёт по показателям</h1>

        <div className="flex items-center gap-4 mb-4">
          <input
            type="month"
            className="border px-3 py-2 rounded"
            value={month}
            onChange={(e) => setMonth(e.target.value)}
          />
          <button
            onClick={fetchReport}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Применить
          </button>
        </div>

        {data && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            {Object.entries(data).map(([key, value]) => (
              <div
                key={key}
                className="border p-3 rounded bg-gray-50 flex justify-between"
              >
                <span className="font-medium">
                  {LABELS_RU[key] || key}
                </span>
                <span>{value}</span>
              </div>
            ))}
          </div>
        )}
      </main>
    </>
  );
}