#pragma once

#ifndef DEBUG_H
#define DEBUG_H

#ifdef DEBUG
    #define debugc(chr) do { fputc(chr, stderr); } while (0)
    #define debugs(str) do { fputs(str, stderr); } while (0)
    #define debugf(...) do { fprintf(stderr, __VA_ARGS__); } while (0)
#else
    #define debugc(chr) do { } while (0)
    #define debugs(str) do { } while (0)
    #define debugf(...) do { } while (0)
#endif

#endif /* DEBUG_H */
