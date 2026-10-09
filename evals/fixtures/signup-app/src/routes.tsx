import { createBrowserRouter } from 'react-router-dom';
import { Dashboard } from './Dashboard';
import { SignupForm } from './SignupForm';
import { Step } from './Step';

// Onboarding: every step is required before the dashboard.
export const router = createBrowserRouter([
  { path: '/signup', element: <SignupForm onDone={() => location.assign('/verify-email')} /> },
  { path: '/verify-email', element: <Step title="Check your inbox" next="/onboarding/company" blocking /> },
  { path: '/onboarding/company', element: <Step title="Company name" next="/onboarding/size" /> },
  { path: '/onboarding/size', element: <Step title="Company size" next="/onboarding/role" /> },
  { path: '/onboarding/role', element: <Step title="Your role" next="/onboarding/avatar" /> },
  { path: '/onboarding/avatar', element: <Step title="Upload a profile photo" next="/onboarding/timezone" /> },
  { path: '/onboarding/timezone', element: <Step title="Your time zone" next="/onboarding/theme" /> },
  { path: '/onboarding/theme', element: <Step title="Pick a theme" next="/onboarding/tour" /> },
  { path: '/onboarding/tour', element: <Step title="Product tour (12 slides)" next="/dashboard" /> },
  { path: '/dashboard', element: <Dashboard /> }
]);
