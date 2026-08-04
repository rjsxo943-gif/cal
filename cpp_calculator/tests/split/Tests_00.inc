#include "ScientificCalculator.h"

#include <cmath>
#include <complex>
#include <exception>
#include <functional>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

// ---- tests/TestHarness.h ----
namespace test {

class Harness {
public:
    void expectTrue(bool condition, const std::string& expression, const char* file, int line) {
        if (!condition) fail(expression, file, line, "expected true"); else ++passed_;
    }

    template <typename Left, typename Right>
    void expectEqual(const Left& left, const Right& right, const std::string& expression,
                     const char* file, int line) {
        if (!(left == right)) {
            std::ostringstream detail;
            detail << "left=" << left << ", right=" << right;
            fail(expression, file, line, detail.str());
        } else {
            ++passed_;
        }
    }

    void expectNear(double left, double right, double tolerance, const std::string& expression,
                    const char* file, int line) {
        if (!std::isfinite(left) || !std::isfinite(right) || std::abs(left - right) > tolerance) {
            std::ostringstream detail;
            detail << "left=" << left << ", right=" << right << ", tolerance=" << tolerance;
            fail(expression, file, line, detail.str());
        } else {
            ++passed_;
        }
    }

    template <typename Exception, typename Callable>
    void expectThrowsMessage(Callable&& callable, const std::string& expected,
                             const std::string& expression, const char* file, int line) {
        try {
            callable();
            fail(expression, file, line, "no exception thrown");
        } catch (const Exception& error) {
            if (std::string(error.what()) != expected) {
                fail(expression, file, line,
                     "message='" + std::string(error.what()) + "', expected='" + expected + "'");
            } else {
                ++passed_;
            }
        } catch (const std::exception& error) {
            fail(expression, file, line, "wrong exception: " + std::string(error.what()));
        }
    }

    int finish() const {
        std::cout << "Passed: " << passed_ << ", Failed: " << failed_ << '\n';
        return failed_ == 0 ? 0 : 1;
    }

private:
    void fail(const std::string& expression, const char* file, int line, const std::string& detail) {
        ++failed_;
        std::cerr << file << ':' << line << " FAILED " << expression << " (" << detail << ")\n";
