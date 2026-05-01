import type { ReactNode } from "react";

interface SectionCardProps {
  title: string;
  eyebrow?: string;
  action?: ReactNode;
  children: ReactNode;
  className?: string;
}

export function SectionCard({ title, eyebrow, action, children, className = "" }: SectionCardProps) {
  return (
    <section className={`rounded-3xl border border-white/10 bg-panel/80 p-6 shadow-glow backdrop-blur ${className}`}>
      <div className="mb-5 flex flex-wrap items-start justify-between gap-4">
        <div>
          {eyebrow ? <p className="text-xs uppercase tracking-[0.24em] text-teal/80">{eyebrow}</p> : null}
          <h2 className="mt-2 font-display text-2xl text-white">{title}</h2>
        </div>
        {action}
      </div>
      {children}
    </section>
  );
}
