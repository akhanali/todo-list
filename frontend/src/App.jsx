import { useEffect, useState } from "react";
import "./index.css";

export default function App() {
  const [todos, setTodos] = useState([]);
  const [title, setTitle] = useState("");

  async function load() {
    const r = await fetch("/api/todos");
    setTodos(await r.json());
  }

  async function addTodo(e) {
    e.preventDefault();
    if (!title.trim()) return;
    await fetch("/api/todos", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title }),
    });
    setTitle("");
    load();
  }

  async function toggle(id, newCompleted, currentTitle) {
    await fetch(`/api/todos/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: currentTitle, completed: newCompleted }),
    });
    load();
  }

  async function del(id) {
    await fetch(`/api/todos/${id}`, { method: "DELETE" });
    load();
  }

  useEffect(() => { load(); }, []);

  return (
    <div className="mx-auto max-w-md p-6">
      <h1 className="text-2xl font-bold text-center mb-6">Todo List</h1>

      <form onSubmit={addTodo} className="flex gap-2 mb-4">
        <input
          className="flex-1 border rounded px-2 py-1"
          placeholder="New task…"
          value={title}
          onChange={e => setTitle(e.target.value)}
        />
        <button className="bg-blue-600 text-white px-3 rounded">Add</button>
      </form>

      <ul className="space-y-2">
        {todos.map(t => (
          <li
            key={t.id}
            className="flex items-center justify-between bg-gray-100 p-2 rounded"
          >
            <span
              onClick={() => toggle(t.id, !t.completed, t.title)}
              className={`cursor-pointer ${t.completed ? "line-through text-gray-500" : ""}`}
            >
              {t.title}
            </span>
            <button
              onClick={() => del(t.id)}
              className="text-red-500 hover:text-red-700"
            >
              ✕
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
