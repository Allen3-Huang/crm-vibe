export interface EventAttendance {
  event_id: string;
  event_name: string;
  date: string;
}

export interface CoursePurchase {
  course_id: string;
  course_name: string;
  date: string;
}

export interface CustomerSummary {
  email: string;
  name: string;
  event_count: number;
  course_count: number;
}

export interface Customer {
  email: string;
  name: string;
  events: EventAttendance[];
  courses: CoursePurchase[];
  event_count: number;
  course_count: number;
}

export interface Event {
  event_id: string;
  event_name: string;
  attendee_count: number;
  attendees: Array<{ name: string; email: string; date: string }>;
}

export interface Course {
  course_id: string;
  course_name: string;
  buyer_count: number;
  buyers: Array<{ name: string; email: string; date: string }>;
}

export interface ConversionStats {
  total_event_attendees: number;
  total_course_buyers: number;
  converted_customers: number;
  conversion_rate: number;
}

export interface EventCourseCorrelation {
  event_id: string;
  event_name: string;
  event_attendees: number;
  converted_to_course: number;
  conversion_rate: number;
  top_courses: Array<{ course_name: string; count: number }>;
}

export interface Analytics {
  total_customers: number;
  total_events: number;
  total_courses: number;
  conversion_stats: ConversionStats;
  event_correlations: EventCourseCorrelation[];
}
