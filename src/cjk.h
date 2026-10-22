#ifndef CMARK_CJK_H
#define CMARK_CJK_H

#include <stdbool.h>
#include "cjk_tables.h"

static bool cmark_cjk_contains(const cmark_cjk_range *ranges, size_t count,
                               int32_t scalar) {
  size_t low = 0, high = count;
  while (low < high) {
    size_t mid = low + (high - low) / 2;
    if (scalar < ranges[mid].first) high = mid;
    else if (scalar > ranges[mid].last) low = mid + 1;
    else return true;
  }
  return false;
}

#define CMARK_CJK_CLASSIFY(name, scalar) \
  cmark_cjk_contains(cmark_cjk_##name##_ranges, \
    sizeof(cmark_cjk_##name##_ranges) / sizeof(cmark_cjk_range), scalar)

static bool cmark_cjk_fullwidth(int32_t base, int32_t selector) {
  size_t count = sizeof(cmark_cjk_fullwidth_pairs) / sizeof(cmark_cjk_range);
  for (size_t i = 0; i < count; ++i) {
    if (cmark_cjk_fullwidth_pairs[i].first == base &&
        cmark_cjk_fullwidth_pairs[i].last == selector) return true;
  }
  return false;
}

/* The matching stack remains cmark's. Only classify delimiter flanking with
 * the opt-in CJK proposal; underscore retains its intraword restriction. */
static void cmark_cjk_flanking(unsigned char marker, int32_t before,
                              int32_t previous_base, int32_t after,
                              bool *can_open, bool *can_close) {
  bool before_space = CMARK_CJK_CLASSIFY(space, before);
  bool after_space = CMARK_CJK_CLASSIFY(space, after);
  bool before_punct = CMARK_CJK_CLASSIFY(punctuation, previous_base);
  bool after_punct = CMARK_CJK_CLASSIFY(punctuation, after);
  bool cjk_neighbor = marker == '*' &&
    (CMARK_CJK_CLASSIFY(cjk, previous_base) ||
     cmark_cjk_fullwidth(previous_base, before) ||
     CMARK_CJK_CLASSIFY(cjk, after));
  bool ideographic_selector = before >= 0xE0100 && before <= 0xE01EF;
  bool left = !after_space && (!after_punct || before_space || before_punct ||
                             cjk_neighbor || (marker == '*' && ideographic_selector));
  bool right = !before_space && (!before_punct || after_space || after_punct || cjk_neighbor);
  *can_open = left && (marker != '_' || !right || before_punct);
  *can_close = right && (marker != '_' || !left || after_punct);
}
#endif
