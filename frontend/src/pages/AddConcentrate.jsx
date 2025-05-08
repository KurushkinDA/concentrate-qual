import React, { useRef, useState } from 'react';
import Header from '../components/Header';
import { apiFetch } from '../api';
import { HotTable } from '@handsontable/react';
import { registerAllModules } from 'handsontable/registry'; 
import 'handsontable/dist/handsontable.full.min.css';

registerAllModules();

export default function AddConcentrate() {
  const hotTableRef = useRef(null);
  const [message, setMessage] = useState('');

  const columns = [
    { data: 'name', type: 'text' },
    { data: 'iron', type: 'text' },
    { data: 'silicon', type: 'text' },
    { data: 'aluminum', type: 'text' },
    { data: 'calcium', type: 'text' },
    { data: 'sulfur', type: 'text' },
    { data: 'report_month', type: 'text' },
  ];

  const handleSave = async () => {
    const hot = hotTableRef.current?.hotInstance;
    if (!hot) return;

    const rows = hot.getData();
    let successCount = 0;
    let failCount = 0;

    for (const row of rows) {
      const [name, iron, silicon, aluminum, calcium, sulfur, report_month] = row;
      if (!name || !report_month) continue;

      try {
        await apiFetch('/concentrates', {
          name,
          iron: Number(iron),
          silicon: Number(silicon),
          aluminum: Number(aluminum),
          calcium: Number(calcium),
          sulfur: Number(sulfur),
          report_month,
        });
        successCount++;
      } catch (err) {
        console.error('Ошибка при добавлении:', err);
        failCount++;
      }
    }

    setMessage(`Добавлено: ${successCount}, ошибок: ${failCount}`);
  };

  return (
    <>
      <Header />
      <main className="p-6">
        <h1 className="text-2xl font-bold mb-4">Добавить показатели</h1>

        <div className="mb-4">
          <HotTable
            ref={hotTableRef}
            data={[{}]}
            colHeaders={[
              'Наименование',
              'Железо',
              'Кремний',
              'Алюминий',
              'Кальций',
              'Сера',
              'Месяц',
            ]}
            columns={columns}
            rowHeaders
            minRows={5}
            stretchH="all"
            contextMenu={['copy', 'cut', 'paste']}
            licenseKey="non-commercial-and-evaluation"
          />
        </div>

        <button
          onClick={handleSave}
          className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
        >
          Сохранить
        </button>

        {message && <p className="mt-4 text-blue-600 text-sm">{message}</p>}
      </main>
    </>
  );
}