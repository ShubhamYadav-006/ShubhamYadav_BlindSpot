import { useState, useRef, useEffect } from "react";
import { Header } from "./components/Header";
import { Hero } from "./components/Hero";
import { DecisionForm } from "./components/DecisionForm";
import { LoadingState } from "./components/LoadingState";
import { ErrorState } from "./components/ErrorState";
import { Results } from "./components/Results";
import { Footer } from "./components/Footer";
import { AnalyzeRequest, AnalyzeResponse } from "./types/analysis";
import { analyzeDecision, ApiError } from "./services/api";

export default function App() {
  const [results, setResults] = useState<AnalyzeResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [lastRequest, setLastRequest] = useState<AnalyzeRequest | null>(null);

  const resultsContainerRef = useRef<HTMLDivElement>(null);
  const formContainerRef = useRef<HTMLDivElement>(null);

  // Accessible auto-scroll / focus when results load
  useEffect(() => {
    if (results && resultsContainerRef.current) {
      resultsContainerRef.current.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
      resultsContainerRef.current.focus({ preventScroll: true });
    }
  }, [results]);

  const handleSubmit = async (requestData: AnalyzeRequest) => {
    if (isLoading) return;

    setIsLoading(true);
    setError(null);
    setLastRequest(requestData);

    try {
      const responseData = await analyzeDecision(requestData);
      setResults(responseData);
    } catch (err: unknown) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An unexpected error occurred while communicating with Blind Spot.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setResults(null);
    setError(null);
    setLastRequest(null);
    setTimeout(() => {
      if (formContainerRef.current) {
        formContainerRef.current.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    }, 50);
  };

  const handleRetry = () => {
    if (lastRequest) {
      handleSubmit(lastRequest);
    } else {
      setError(null);
    }
  };

  return (
    <div className="min-h-screen bg-base text-text-primary flex flex-col selection:bg-accent-primary selection:text-white font-sans antialiased">
      {/* 1. Header with brand and theme toggle */}
      <Header />

      {/* 2. Main Content Area */}
      <main className="flex-1 py-6 sm:py-10 space-y-8">
        {!results && !isLoading && !error && (
          <div ref={formContainerRef} className="space-y-6 sm:space-y-10">
            <Hero />
            <DecisionForm onSubmit={handleSubmit} isLoading={isLoading} />
          </div>
        )}

        {/* 3. Skeleton Loading State */}
        {isLoading && <LoadingState />}

        {/* 4. Error State with Retry */}
        {error && !isLoading && (
          <ErrorState message={error} onRetry={handleRetry} />
        )}

        {/* 5. Results View */}
        {results && !isLoading && (
          <div
            ref={resultsContainerRef}
            tabIndex={-1}
            className="outline-none focus:outline-none"
            aria-live="polite"
          >
            <Results data={results} onReset={handleReset} />
          </div>
        )}
      </main>

      {/* 6. Footer */}
      <Footer />
    </div>
  );
}
