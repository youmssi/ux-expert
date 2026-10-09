import { api } from './api';

export function ProjectMenu({ projectId, onDeleted }: { projectId: string; onDeleted: () => void }) {
  const remove = async () => {
    await api.deleteProject(projectId);
    onDeleted();
  };

  return (
    <div className="menu">
      <button onClick={() => api.renameProject(projectId)}>Rename</button>
      <button onClick={remove}>Delete</button>
    </div>
  );
}
