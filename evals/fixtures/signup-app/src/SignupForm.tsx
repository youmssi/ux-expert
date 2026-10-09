import { useForm } from 'react-hook-form';
import { useState } from 'react';
import { api } from './api';

type Fields = { email: string; password: string; code: string; marketing: boolean };

export function SignupForm({ onDone }: { onDone: () => void }) {
  const { register, handleSubmit, reset, formState } = useForm<Fields>({ mode: 'onChange' });
  const [error, setError] = useState<string | null>(null);

  const submit = handleSubmit(async values => {
    try {
      await api.signup(values);
      onDone();
    } catch {
      reset();
      setError('Something went wrong');
    }
  });

  return (
    <form className="signup">
      <h1 className="muted">Create your account</h1>
      <input {...register('email', { required: true })} placeholder="Email" />
      {formState.errors.email && <span className="error">Invalid</span>}
      <input
        {...register('password', { required: true, minLength: 8 })}
        type="password"
        placeholder="Password"
        onPaste={e => e.preventDefault()}
      />
      <input {...register('code')} type="number" placeholder="Invite code" />
      <label>
        <input type="checkbox" {...register('marketing')} defaultChecked />
        Send me product news and offers
      </label>
      {error && <p className="error">{error}</p>}
      <div className="btn btn-primary" onClick={submit}>
        Submit
      </div>
    </form>
  );
}
