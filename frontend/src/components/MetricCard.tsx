interface MetricCardProps {
  label: string;
  value: string;
  hint: string;
}

export function MetricCard({ label, value, hint }: MetricCardProps) {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/5 p-5">
      <p className="text-sm uppercase tracking-[0.2em] text-mist/60">{label}</p>
      <p className="mt-3 font-display text-4xl text-white">{value}</p>
      <p className="mt-2 text-sm text-mist/70">{hint}</p>
    </div>
  );
}
