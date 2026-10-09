import { useForm } from 'react-hook-form';
import { api } from './api';
import './login.css';

type Fields = { email: string; password: string };

export function LoginForm({ onDone }: { onDone: () => void }) {
  const { register, handleSubmit, formState } = useForm<Fields>();

  const submit = handleSubmit(async values => {
    await api.login(values);
    onDone();
  });

  return (
    <form onSubmit={submit} noValidate>
      <label htmlFor="login-email">Email</label>
      <input id="login-email" type="email" autoComplete="email" aria-describedby="login-email-error" {...register('email', { required: true })} />
      {formState.errors.email && (
        <p id="login-email-error" role="alert">
          Enter your email address, like name@company.com
        </p>
      )}
      <label htmlFor="login-password">Password</label>
      <input id="login-password" type="password" autoComplete="current-password" {...register('password', { required: true })} />
      <button type="submit" className="focus-ring">
        Sign in
      </button>
    </form>
  );
}
