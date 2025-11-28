// Completely silence React hydration + Next.js console errors
if (typeof window !== "undefined") {
  const ignored = [
    "A tree hydrated but some attributes",
    "Expected server HTML to contain",
    "Hydration failed",
    "Text content does not match",
  ];

  const originalError = console.error;
  console.error = (...args) => {
    if (ignored.some(msg => (args[0] || "").includes(msg))) return;
    originalError(...args);
  };
}
