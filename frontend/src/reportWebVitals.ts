// src/reportWebVitals.ts

// Import necessary functions from web-vitals
import { onCLS, onFID, onFCP, onLCP, onTTFB } from 'web-vitals';

// Define the type for the performance entry handler
type ReportHandler = (metric: {
  name: string;
  value: number;
  delta: number;
  id: string;
  entries: PerformanceEntry[];
}) => void;

// Function to report web vitals
const reportWebVitals = (onPerfEntry?: ReportHandler) => {
  if (onPerfEntry && onPerfEntry instanceof Function) {
    onCLS(onPerfEntry);
    onFID(onPerfEntry);
    onFCP(onPerfEntry);
    onLCP(onPerfEntry);
    onTTFB(onPerfEntry);
  }
};

export default reportWebVitals;
