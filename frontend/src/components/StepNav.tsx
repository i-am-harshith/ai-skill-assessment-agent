import { NavLink } from "react-router-dom";

const steps = [
  { to: "/", label: "Home" },
  { to: "/job-description", label: "Job Description" },
  { to: "/resume", label: "Resume" },
  { to: "/analysis", label: "Gap Analysis" },
  { to: "/assessment", label: "Assessment" },
  { to: "/report", label: "Final Report" },
];

export function StepNav() {
  return (
    <nav className="flex flex-wrap gap-2">
      {steps.map((step) => (
        <NavLink
          key={step.to}
          to={step.to}
          className={({ isActive }) =>
            `rounded-full px-4 py-2 text-sm transition ${
              isActive ? "bg-teal text-ink" : "border border-white/10 bg-white/5 text-mist/70 hover:text-white"
            }`
          }
        >
          {step.label}
        </NavLink>
      ))}
    </nav>
  );
}
