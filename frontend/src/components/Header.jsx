import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { apiFetch } from '../api';

export default function Header() {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await apiFetch('/users/logout', {
        method: 'POST',
      });
      navigate('/login');
    } catch (err) {
      console.error('Ошибка при выходе из аккаунта:', err.message);
    }
  };

  return (
    <header className="bg-gray-800 text-white px-6 py-4 flex justify-between items-center">
      <nav className="flex gap-4">
        <Link to="/" className="hover:underline">Показатели</Link>
        <Link to="/report" className="hover:underline">Отчёт</Link>
        <Link to="/add" className="hover:underline">Добавить</Link>
      </nav>
      <button onClick={handleLogout} className="hover:underline">Выход</button>
    </header>
  );
}