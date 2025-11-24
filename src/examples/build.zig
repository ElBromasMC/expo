const std = @import("std");

const OmpPaths = struct {
    include: ?[]const u8 = null,
    lib: ?[]const u8 = null,
};

fn findLlvmOmp(b: *std.Build) OmpPaths {
    var best: ?struct { prefix: []const u8, ver: i32 } = null;
    if (std.fs.cwd().openDir("/usr/lib", .{ .iterate = true })) |dir| {
        var it = dir.iterate();
        while (it.next() catch null) |entry| {
            if (entry.kind != .directory) continue;
            if (!std.mem.startsWith(u8, entry.name, "llvm-")) continue;
            const ver_str = entry.name["llvm-".len..];
            const ver = std.fmt.parseInt(i32, ver_str, 10) catch continue;
            if (best == null or ver > best.?.ver) best = .{ .prefix = b.dupe(entry.name), .ver = ver };
        }
    } else |_| {}

    var paths = OmpPaths{};
    if (best) |llvm| {
        const prefix = b.fmt("/usr/lib/{s}", .{llvm.prefix});
        const include_path = b.fmt("{s}/lib/clang/{d}/include", .{ prefix, llvm.ver });
        if (std.fs.accessAbsolute(include_path, .{})) |_| {
            paths.include = include_path;
        } else |_| {}
        const lib_path = b.fmt("{s}/lib", .{prefix});
        if (std.fs.accessAbsolute(lib_path, .{})) |_| {
            paths.lib = lib_path;
        } else |_| {}
    }
    if (b.graph.env_map.get("LIBOMP_INCLUDE")) |inc| paths.include = inc;
    if (b.graph.env_map.get("LIBOMP_LIB")) |lib| paths.lib = lib;
    return paths;
}

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});
    const is_windows = target.result.os.tag == .windows;
    const is_windows_gnu = is_windows and target.result.abi == .gnu;

    const all = b.step("run", "Compila y ejecuta (en host) los ejemplos disponibles");

    // pthreads (POSIX y se permite compilar en windows-gnu aunque no se ejecute)
    if (!is_windows or is_windows_gnu) {
        const pthreads_mod = b.createModule(.{
            .root_source_file = null,
            .target = target,
            .optimize = optimize,
            .link_libc = true,
        });
        pthreads_mod.addCSourceFile(.{
            .file = b.path("pthreads_matrix.c"),
            .flags = &.{ "-pthread" },
        });
        const pthreads = b.addExecutable(.{
            .name = "pthreads_matrix",
            .root_module = pthreads_mod,
        });
        b.installArtifact(pthreads);

        const pthreads_step = b.step("pthreads", "Compila pthreads_matrix");
        pthreads_step.dependOn(&pthreads.step);
        pthreads_step.dependOn(b.getInstallStep());

        const run_pthreads_step = b.step("run-pthreads", "Ejecuta pthreads_matrix (solo target nativo)");
        run_pthreads_step.dependOn(pthreads_step);
        if (target.query.isNative()) {
            const run_pthreads = b.addRunArtifact(pthreads);
            run_pthreads.step.dependOn(b.getInstallStep());
            run_pthreads_step.dependOn(&run_pthreads.step);
        }

        all.dependOn(run_pthreads_step);
    }

    // OpenMP (POSIX y opcionalmente windows-gnu si se suministra runtime).
    if (!is_windows or is_windows_gnu) {
        var omp_paths = findLlvmOmp(b);
        if (is_windows_gnu and omp_paths.include == null and omp_paths.lib == null) {
            omp_paths.include = "libs/mingw64/include";
            omp_paths.lib = "libs/mingw64/lib";
        }
        const openmp_mod = b.createModule(.{
            .root_source_file = null,
            .target = target,
            .optimize = optimize,
            .link_libc = true,
        });
        if (omp_paths.include) |inc| {
            openmp_mod.addSystemIncludePath(.{ .src_path = .{ .owner = b, .sub_path = inc } });
        }
        if (omp_paths.lib) |lib_dir| {
            openmp_mod.addLibraryPath(.{ .src_path = .{ .owner = b, .sub_path = lib_dir } });
            openmp_mod.addRPath(.{ .src_path = .{ .owner = b, .sub_path = lib_dir } });
        }
        openmp_mod.addCSourceFile(.{
            .file = b.path("openmp_matrix.c"),
            .flags = &.{ "-fopenmp", "-std=gnu11" },
        });
        if (is_windows_gnu) {
            // Forzar ruta MinGW y link a libomp.dll.a
            openmp_mod.addObjectFile(.{ .src_path = .{ .owner = b, .sub_path = "libs/mingw64/lib/libomp.dll.a" } });
            openmp_mod.addLibraryPath(.{ .src_path = .{ .owner = b, .sub_path = "libs/mingw64/lib" } });
        }
        openmp_mod.linkSystemLibrary("omp", .{});

        const openmp = b.addExecutable(.{
            .name = "openmp_matrix",
            .root_module = openmp_mod,
        });
        b.installArtifact(openmp);
        if (is_windows_gnu) {
            const dll_install = b.addInstallBinFile(b.path("libs/mingw64/bin/libomp.dll"), "libomp.dll");
            const pthread_dll = b.addInstallBinFile(b.path("libs/mingw64/bin/libwinpthread-1.dll"), "libwinpthread-1.dll");
            const gcc_dll = b.addInstallBinFile(b.path("libs/mingw64/bin/libgcc_s_seh-1.dll"), "libgcc_s_seh-1.dll");
            b.getInstallStep().dependOn(&dll_install.step);
            b.getInstallStep().dependOn(&pthread_dll.step);
            b.getInstallStep().dependOn(&gcc_dll.step);
        }

        const openmp_step = b.step("openmp", "Compila openmp_matrix");
        openmp_step.dependOn(&openmp.step);
        openmp_step.dependOn(b.getInstallStep());

        const run_openmp_step = b.step("run-openmp", "Ejecuta openmp_matrix (solo target nativo)");
        run_openmp_step.dependOn(openmp_step);
        if (target.query.isNative()) {
            const run_openmp = b.addRunArtifact(openmp);
            run_openmp.step.dependOn(b.getInstallStep());
            run_openmp_step.dependOn(&run_openmp.step);
        }

        all.dependOn(run_openmp_step);
    }
}
