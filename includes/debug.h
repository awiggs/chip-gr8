#pragma once

#ifndef DEBUG_H
#define DEBUG_H

#define SAFE_MACRO(expr) do { expr } while(0)

#ifdef DEBUG
    #define debugc(chr) SAFE_MACRO({ fputc(chr, stderr); })
    #define debugs(str) SAFE_MACRO({ fputs(str, stderr); })
    #define debugf(...) SAFE_MACRO({ fprintf(stderr, __VA_ARGS__); })
#else
    #define debugc(chr) ;
    #define debugs(str) ;
    #define debugf(...) ;
#endif

/**
 * A formatted print function that prints to standard error and then exits the
 * program.
 */
#define panic(...) SAFE_MACRO({ \
    fflush(stdout); \
    fflush(stderr); \
    fprintf(stderr, "\npanic! "); \
    fprintf(stderr, __VA_ARGS__); \
    fprintf(stderr, "\n"); \
    fflush(stderr); \
    exit(1); \
})

#endif /* DEBUG_H */
