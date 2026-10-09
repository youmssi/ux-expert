import { useEffect, useState } from 'react';
import { api, Project } from './api';
import { ProjectMenu } from './ProjectMenu';

export function Dashboard() {
  const [projects, setProjects] = useState<Project[] | null>(null);

  useEffect(() => {
    api
      .listProjects()
      .then(setProjects)
      .catch(() => {});
  }, []);

  if (projects === null) {
    return <div className="spinner" />;
  }

  return (
    <main>
      <img src="/logo.png" />
      <ul>
        {projects.map(p => (
          <li key={p.id}>
            {p.name}
            <ProjectMenu projectId={p.id} onDeleted={() => setProjects(projects.filter(x => x.id !== p.id))} />
          </li>
        ))}
      </ul>
    </main>
  );
}
