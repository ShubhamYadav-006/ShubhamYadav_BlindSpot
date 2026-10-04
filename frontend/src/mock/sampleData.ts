import { AnalyzeResponse } from "../types/analysis";

/**
 * Realistic demonstration mock data used for development and previewing.
 */
export const SAMPLE_ANALYSIS_DATA: AnalyzeResponse = {
  decision: "Accept the 6-month startup internship in Bangalore over continuing college coursework locally.",
  stated_factors: [
    { factor: "₹45,000 monthly stipend and travel allowance", category: "money" },
    { factor: "Direct mentorship under former big-tech engineering leads", category: "career" },
    { factor: "Rapid hands-on experience building production AI pipelines", category: "growth" },
    { factor: "Relocation required 1,200 km away from home and college", category: "convenience" },
  ],
  assumptions: [
    {
      assumption: "College administration will grant attendance waivers without delay.",
      why_risky: "University credit transfer or attendance policies may be rigid, risking an academic backlog.",
    },
    {
      assumption: "The early-stage startup has sufficient runway to honor the full 6-month commitment.",
      why_risky: "Early-stage ventures occasionally face sudden funding pivots or structural shifts.",
    },
  ],
  conflicts: [
    {
      conflict: "Prioritizing immediate career growth vs maintaining academic GPA standing",
      explanation: "Full-time startup workload (50+ hrs/wk) directly competes with semester exam preparations.",
    },
  ],
  blind_spots: [
    {
      area: "Hidden Net Cost of Relocation & Living",
      why_it_matters_for_you: "Bangalore rent, deposit, and daily commute may consume over 60% of the stipend, reducing your expected financial cushion.",
    },
    {
      area: "Academic Re-entry Friction",
      why_it_matters_for_you: "Taking a semester away might isolate you from project groups and placement cycles returning the following term.",
    },
    {
      area: "Mentorship Availability vs Startup Firefighting",
      why_it_matters_for_you: "In pre-seed startups, senior engineers often spend 90% of their time fixing critical bugs rather than structured mentoring.",
    },
  ],
  questions: [
    {
      question: "Agar college ne formal NOC/attendance waiver deny kar diya, toh tumhara fallback plan kya hai?",
      linked_to: "Assumption on college waivers",
    },
    {
      question: "Living cost calculate karne ke baad, kya remaining savings tumhare financial goals ko justify karti hai?",
      linked_to: "Hidden Net Cost of Relocation",
    },
    {
      question: "Interview rounds mein kya tumne specific examples dekhe jahan interns ko structured learning mil rahi thi?",
      linked_to: "Mentorship Availability vs Firefighting",
    },
    {
      question: "Agar dono options ka immediate stipend same hota, toh kya tum phir bhi relocate karne ka decision lete?",
      linked_to: "Conflict between growth and academic standing",
    },
    {
      question: "6 months baad jab yeh internship khatam hogi, tumhara agla target step kya hoga aur yeh role usmein kaise help karega?",
      linked_to: "Career growth expectation",
    },
  ],
};
