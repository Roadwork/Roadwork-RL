class Bucket {
    constructor(bucketCount, rangeLow, rangeHigh) {
      this.bucketCount = bucketCount;
      this.rangeLow = rangeLow;
      this.rangeHigh = rangeHigh;
      this.stepSize = (Math.abs(rangeLow) + Math.abs(rangeHigh)) / bucketCount;
      this.buckets = [];
  
      // For easiness we include the indexes
      this.bucketIndexes = [];
  
      for (let i = 0; i < bucketCount; i++) {
        this.bucketIndexes.push(i);
      }
  
      this.initBuckets();
    }
  
    initBuckets() {
      for (let i = 0; i < this.bucketCount; i++) {
        this.buckets[i] = [];
      }
    }
  
    addValueToBucket(val) {
      let idx = this.getBucketIdxForValue(val);
      this.buckets[idx].push(val);
    }
  
    getBucketIdxForValue(val) {
      let idx = 0;
  
      // Find bucket, put values on the outer size of the range in the last bucket
      while ((idx < this.bucketCount - 1) && val > this.rangeLow + this.stepSize * (idx + 1)) {
        idx++;
      }
  
      return idx;
    }
  }
  
  module.exports = Bucket;