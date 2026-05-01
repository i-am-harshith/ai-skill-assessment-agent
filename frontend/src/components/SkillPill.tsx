export function SkillPill({
  label,
  tone = "neutral",
}: {
  label: string;
  tone?: "neutral" | "good" | "warn" | "alert";
}) {
  const toneClass =
    tone === "good"
      ? "border-teal/30 bg-teal/10 text-teal"
      : tone === "warn"
        ? "border-sand/30 bg-sand/10 text-sand"
        : tone === "alert"
          ? "border-coral/30 bg-coral/10 text-coral"
          : "border-white/10 bg-white/5 text-mist";

  return <span className={`rounded-full border px-3 py-1 text-sm ${toneClass}`}>{label}</span>;
}
