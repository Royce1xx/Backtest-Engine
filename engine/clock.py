# backtestr/engine/clock.py
class Clock:
    """
    Manages time progression in the backtest.
    """
    
    def __init__(self, timeline):
        """
        Initialize clock with a timeline.
        
        Args:
            timeline: List of timestamps to iterate through
        """
        self.timeline = timeline
        self.current_index = 0
    
    def __iter__(self):
        """Make clock iterable."""
        return self
    
    def __next__(self):
        """Get next timestamp."""
        if self.current_index >= len(self.timeline):
            raise StopIteration
        
        timestamp = self.timeline[self.current_index]
        self.current_index += 1
        return timestamp
    
    def has_next(self):
        """Check if there are more timestamps."""
        return self.current_index < len(self.timeline)
    
    def next(self):
        """Get next timestamp (legacy method)."""
        return self.__next__()
    
    def reset(self):
        """Reset clock to beginning."""
        self.current_index = 0
    
    def get_current_timestamp(self):
        """Get current timestamp."""
        if self.current_index > 0 and self.current_index <= len(self.timeline):
            return self.timeline[self.current_index - 1]
        return None
