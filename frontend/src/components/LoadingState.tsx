export function LoadingState({ label = "Loading..." }: { label?: string }) {
  return (
    <div className="flex min-h-[200px] items-center justify-center rounded-3xl border border-white/10 bg-panel/60 p-6">
      <div className="flex items-center gap-3 text-mist/80">
        <span className="h-3 w-3 animate-pulse rounded-full bg-teal" />
        <span>{label}</span>
      </div>
    </div>
  );
}
