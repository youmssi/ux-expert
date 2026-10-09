export type Project = { id: string; name: string };

async function call<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`/api${path}`, init);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return (await response.json()) as T;
}

export const api = {
  signup: (body: unknown) => call<void>('/signup', { method: 'POST', body: JSON.stringify(body) }),
  login: (body: unknown) => call<void>('/login', { method: 'POST', body: JSON.stringify(body) }),
  listProjects: () => call<Project[]>('/projects'),
  renameProject: (id: string) => call<void>(`/projects/${id}/rename`, { method: 'POST' }),
  deleteProject: (id: string) => call<void>(`/projects/${id}`, { method: 'DELETE' })
};
